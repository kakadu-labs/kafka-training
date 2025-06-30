use std::time::Duration;

use axum::{
    Json, Router,
    http::StatusCode,
    response::Response,
    routing::{get, post},
};
use chrono::{DateTime, Utc};
use rand::Rng;
use reqwest;
use rust_decimal::prelude::*;
use serde::{Deserialize, Serialize};
use tracing;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let app = Router::new()
        .route("/", get(StatusCode::OK))
        .route("/health", get(health))
        .route("/transaction", post(transaction_handler));

    // run our app with hyper, listening globally on port 3000
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn health() -> Response<String> {
    Response::builder().body(String::from("World")).unwrap()
}

async fn transaction_handler(Json(transaction): Json<Transaction>) -> StatusCode {
    tracing::info!("Transcation post! {:?}", transaction);
    let mut rng = rand::rng();
    let sleep_random: u64 = rng.random_range(0..=45);
    tracing::info!("Sleeping: {:?}", &sleep_random);
    std::thread::sleep(Duration::from_secs(sleep_random));
    if rng.random_range(0..=1000) > 990 {
        return StatusCode::INTERNAL_SERVER_ERROR;
    }
    if transaction.amount > Decimal::from(100) {
        tokio::spawn(async move {
            send_telegram(transaction).await;
        });
    }
    StatusCode::OK
}

#[derive(Debug, Serialize, Deserialize)]
struct Transaction {
    name: String,
    amount: Decimal,
    timestamp: DateTime<Utc>,
}

async fn send_telegram(transaction: Transaction) {
    tracing::info!("Sending Telegram message");
    // You'll need to set your bot token and chat ID
    let bot_token =
        std::env::var("TELEGRAM_BOT_TOKEN").unwrap_or_else(|_| "your_bot_token_here".to_string());
    let chat_id =
        std::env::var("TELEGRAM_CHAT_ID").unwrap_or_else(|_| "your_chat_id_here".to_string());

    let message = format!(
        "🚨 High-value transaction detected!\n\n\
        Name: {}\n\
        Amount: ${}\n\
        Timestamp: {}\n\
        \nTransaction processed successfully.",
        transaction.name,
        transaction.amount,
        transaction.timestamp.format("%Y-%m-%d %H:%M:%S UTC")
    );

    let url = format!("https://api.telegram.org/bot{}/sendMessage", bot_token);

    let payload = serde_json::json!({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    });

    match reqwest::Client::new()
        .post(&url)
        .json(&payload)
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                tracing::info!("Telegram message sent successfully");
            } else {
                tracing::error!(
                    "Failed to send Telegram message: {}, {}",
                    response.status(),
                    response.text().await.unwrap()
                );
            }
        }
        Err(e) => {
            tracing::error!("Error sending Telegram message: {}", e);
        }
    }
}
