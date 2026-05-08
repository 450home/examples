use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_service;

/// A simple Spin HTTP component.
#[http_service]
async fn goodbye_world(req: Request) -> impl IntoResponse {
    println!("{:?}", req.headers());
    Response::builder()
        .status(200)
        .header("foo", "bar")
        .body("Goodbye, Fermyon!\n".to_string())
}
