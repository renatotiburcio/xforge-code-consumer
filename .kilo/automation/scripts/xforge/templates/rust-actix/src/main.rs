use actix_web::{get, web, App, HttpServer, Responder};

#[get("/")]
async fn hello() -> impl Responder {
    web::Json(serde_json::json!({"message": "Hello XForge!"}))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(hello))
        .bind("127.0.0.1:8080")?
        .run()
        .await
}
