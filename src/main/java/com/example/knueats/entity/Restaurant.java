package com.example.knueats.entity;

import lombok.*;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;

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
   // private String description;

    private String tel;
    private String address;

    private float lat;

    private float lon; //위도경도

    private String menu; //나중에 Menu menu로 변경
    private String category;
    ; // tag enum

    @Builder
    public Restaurant(String name, String tel, String menu, float lat, float lon, String category) {
        this.name = name;
        this.tel = tel;
        this.menu = menu;
        this.lat = lat;
        this.lon = lon;
        this.category = category;
    }


}