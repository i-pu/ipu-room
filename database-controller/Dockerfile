FROM rust:1.35 as builder

WORKDIR /usr/src/database-controller

RUN apt-get update && \
    apt-get install musl-tools -y && \
    rustup target add x86_64-unknown-linux-musl && \
    mkdir src && \
    echo "fn main() {println!(\"if you see this, the build broke\")}" > src/main.rs

COPY Cargo.toml ./

RUN RUSTFLAGS=-Clinker=musl-gcc cargo build --release --target=x86_64-unknown-linux-musl
RUN rm -rf /usr/src/database-controller/target/x86_64-unknown-linux-musl/release/database-controller
RUN rm -f /usr/src/database-controller/target/x86_64-unknown-linux-musl/release/deps/database-controller*
RUN rm -rf src/

COPY src src/
COPY diesel.toml .
RUN RUSTFLAGS=-Clinker=musl-gcc cargo build --release --target=x86_64-unknown-linux-musl


FROM alpine:3.9

RUN apk add --no-cache libpq postgresql-client

COPY --from=builder /usr/src/database-controller/target/x86_64-unknown-linux-musl/release/database-controller /usr/local/bin/database-controller

COPY entry.sh ./

USER nobody
CMD ["./entry.sh" , "database-controller"]
