package com.example.knueats.entity;

import lombok.*;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;
import java.util.List;

@Getter
@Setter
@Entity
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EntityListeners(AuditingEntityListener.class)
public class Restaurant {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String description;
    private String tel;
    private String address;
    private float lat;
    private float lon; //위도경도
    private String location;
    private String category;
    private String menu;
    private float score;
    private int review;
    ; // tag enum
    @Builder
    public Restaurant(String name,String description, String tel,float lat,float lon, String address, String category, String location,float score,int review) {
        this.name = name;
        this.description = description;
        this.tel = tel;
        this.address = address;
        this.category = category;
        this.location = location;
        this.lat = lat;
        this.lon = lon;
        this.score = score;
        this.review = review;
    }
}