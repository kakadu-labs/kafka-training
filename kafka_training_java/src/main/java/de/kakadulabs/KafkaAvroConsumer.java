package de.kakadulabs;

import org.apache.avro.generic.GenericRecord;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class KafkaAvroConsumer {

    public static void main(String[] args) {
        Properties properties = new Properties();
        // normal consumer
        properties.setProperty("bootstrap.servers", "116.203.255.71:9092");
        properties.setProperty("group.id", "customer-consumer-group-v2");
        properties.setProperty("auto.offset.reset", "earliest");

        // avro part
        properties.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        properties.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        properties.setProperty("schema.registry.url", "http://116.203.255.71:7081");

        //.setProperty("specific.avro.reader", "true");

        KafkaConsumer<String, GenericRecord> kafkaConsumer = new KafkaConsumer<>(properties);
        String topic = "credit-card-transactions-avro";
        kafkaConsumer.subscribe(Collections.singleton(topic));

        System.out.println("Waiting for data...");

        while (true){
            ConsumerRecords<String, GenericRecord> records = kafkaConsumer.poll(Duration.ofMillis(500));
            try {
                for (ConsumerRecord<String, GenericRecord> record : records){
                    GenericRecord customer = record.value();
                    System.out.println(customer);
                }
            } catch (Exception e) {
                System.out.println("Exception!");
                // TODO graceful error Handling!
            }


            kafkaConsumer.commitSync();
        }

    }
}