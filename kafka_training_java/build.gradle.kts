plugins {
    id("java")
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
    maven { url = uri("https://packages.confluent.io/maven/" )}

}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    implementation("org.apache.kafka:kafka-clients:4.0.0")
    implementation("io.confluent:kafka-avro-serializer:8.0.0")
    implementation("org.slf4j:slf4j-api:1.7.25")
    implementation("org.slf4j:slf4j-simple:1.6.1")
    implementation("org.apache.kafka:kafka-streams:4.0.0")
    implementation("io.confluent:kafka-streams-avro-serde:8.0.0")
}

tasks.test {
    useJUnitPlatform()
}