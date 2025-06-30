# Build stage
FROM rust:1.88-alpine AS builder

# Install build dependencies
RUN apk add --no-cache libc-dev openssl-dev build-base musl-dev pkgconfig openssl-libs-static

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

# Build the application
RUN cargo build --release

# Runtime stage
FROM alpine:latest

# Install runtime dependencies
RUN apk add --no-cache ca-certificates

WORKDIR /app

# Copy the binary from builder stage
COPY --from=builder /app/target/release/external_service_mock .

# Expose port
EXPOSE 3000

# Run the application
CMD ["./external_service_mock"]
