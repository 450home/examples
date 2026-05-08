package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"plugin"
)

const (
	templatePath           = "/uk/libukp/template_instance"
	scaleToZeroDisablePath = "/uk/libukp/scale_to_zero_disable"
	romSourcePath          = "/rom/rom.go"
	romBuildDir            = "/run/rombuild"
	romPluginPath          = "/run/rom.so"
)

var romHandler func() string

func setScaleToZeroDisabled(disabled bool) error {
	value := []byte("-")
	if disabled {
		value = []byte("+")
	}

	if err := os.WriteFile(scaleToZeroDisablePath, value, 0o644); err != nil {
		return fmt.Errorf("writing %s: %w", scaleToZeroDisablePath, err)
	}

	return nil
}

func loadROMModule() error {
	// Set up a temporary module directory to build the ROM plugin.
	if err := os.MkdirAll(romBuildDir, 0o755); err != nil {
		return fmt.Errorf("creating ROM build dir: %w", err)
	}

	src, err := os.ReadFile(romSourcePath)
	if err != nil {
		romHandler = func() string {
			return "No code loaded\n"
		}
		return nil
	}
	if err = os.WriteFile(romBuildDir+"/rom.go", src, 0o644); err != nil {
		return fmt.Errorf("staging ROM source: %w", err)
	}
	goMod := "module rommod\n\ngo 1.26\n"
	if err = os.WriteFile(romBuildDir+"/go.mod", []byte(goMod), 0o644); err != nil {
		return fmt.Errorf("writing go.mod: %w", err)
	}

  // Disable scale-to-zero while building the plugin, as it can take a few
  // seconds and we don't want the instance to be scaled down in the meantime.
	if err = setScaleToZeroDisabled(true); err != nil {
		return fmt.Errorf("disabling scale-to-zero: %w", err)
	}
	defer func() {
		if restoreErr := setScaleToZeroDisabled(false); restoreErr != nil {
			log.Printf("warning: failed to re-enable scale-to-zero: %v", restoreErr)
		}
	}()

	// Compile the ROM source to a native plugin.
	cmd := exec.Command("go", "build", "-buildmode=plugin", "-o", romPluginPath, ".")
	cmd.Dir = romBuildDir
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err = cmd.Run(); err != nil {
		return fmt.Errorf("compiling ROM plugin: %w", err)
	}
	log.Printf("compiled ROM plugin to %s", romPluginPath)

	p, err := plugin.Open(romPluginPath)
	if err != nil {
		return fmt.Errorf("opening ROM plugin: %w", err)
	}

	sym, err := p.Lookup("Handler")
	if err != nil {
		return fmt.Errorf("looking up Handler symbol: %w", err)
	}

	handler, ok := sym.(func() string)
	if !ok {
		return fmt.Errorf("Handler has unexpected type")
	}
	romHandler = handler

	log.Printf("loaded ROM module from %s", romSourcePath)
	return nil
}

func writeTemplateFlag() {
	if err := os.WriteFile(templatePath, []byte("1"), 0o644); err != nil {
		log.Printf("warning: failed to write template flag: %v", err)
	}
}

func main() {
	host := flag.String("host", "0.0.0.0", "listen host")
	port := flag.Int("port", 8080, "listen port")
	flag.Parse()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
			return
		}
		w.Header().Set("Content-Type", "text/plain")
		fmt.Fprint(w, romHandler())
	})

	addr := fmt.Sprintf("%s:%d", *host, *port)
	srv := &http.Server{Addr: addr}

	// Initiate template creation right before loading the ROM module
	fmt.Println("writing template flag")
	writeTemplateFlag()

	if err := loadROMModule(); err != nil {
		log.Fatalf("failed to load ROM module: %v", err)
	}

	log.Printf("starting server at %s", addr)
	if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("server error: %v", err)
	}
}
