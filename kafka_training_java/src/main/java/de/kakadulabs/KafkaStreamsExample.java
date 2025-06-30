package de.kakadulabs;
import org.apache.avro.generic.GenericRecord;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import io.confluent.kafka.streams.serdes.avro.GenericAvroSerde;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Collections;
import java.util.Map;
import java.util.Properties;


public class KafkaStreamsExample {
    public static void main(String[] args) {
        final Properties streamsConfiguration = new Properties();
        streamsConfiguration.put(StreamsConfig.APPLICATION_ID_CONFIG, "avro-example");
        streamsConfiguration.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "116.203.255.71:9092");
        streamsConfiguration.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        streamsConfiguration.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, GenericAvroSerde.class);
        streamsConfiguration.put("schema.registry.url", "http://116.203.255.71:7081");

        final Map<String, String> serdeConfig = Collections.singletonMap("schema.registry.url",
                "http://116.203.255.71:7081");

        final Serde<String> keyStringSerde = Serdes.String();
        keyStringSerde.configure(serdeConfig, true);

        final Serde<GenericRecord> valueGenericAvroSerde = new GenericAvroSerde();
        valueGenericAvroSerde.configure(serdeConfig, false);

        StreamsBuilder builder = new StreamsBuilder();

        // Use GenericRecord instead of Bar
        KStream<String, GenericRecord> stream = builder.stream("credit-card-transactions-avro",
                Consumed.with(keyStringSerde, valueGenericAvroSerde));

        // Process the stream and extract fields
        stream.foreach((key, value) -> {
            // Extract fields from the GenericRecord
            Long timestamp = (Long) value.get("timestamp");
            Long ccNum = (Long) value.get("cc_num");
            String merchant = value.get("merchant").toString();
            String category = value.get("category").toString();
            Double amount = (Double) value.get("amt");
            String firstName = value.get("first").toString();
            String lastName = value.get("last").toString();
            String country = value.get("country").toString();

            System.out.println("Key: " + key);
            System.out.println("Timestamp: " + timestamp);
            System.out.println("CC Number: " + ccNum);
            System.out.println("Merchant: " + merchant);
            System.out.println("Category: " + category);
            System.out.println("Amount: " + amount);
            System.out.println("Name: " + firstName + " " + lastName);
            System.out.println("Country: " + country);
            System.out.println("---");
        });

        final KafkaStreams streams = new KafkaStreams(builder.build(), streamsConfiguration);
        streams.start();

        // Add shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
