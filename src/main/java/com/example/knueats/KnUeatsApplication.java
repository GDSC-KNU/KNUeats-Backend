package com.example.knueats;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@EnableJpaAuditing
@SpringBootApplication
public class KnUeatsApplication {

	public static void main(String[] args) {
		SpringApplication.run(KnUeatsApplication.class, args);
	}

}
