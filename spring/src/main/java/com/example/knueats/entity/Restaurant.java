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
    private String description;
    private String tel;
    private String address;
    private float lat;
    private float lon; //위도경도
    private String location;
    private String menu; //나중에 Menu menu로 변경
    private String category;
    private float score;
    private int review;
    ; // tag enum
    @Builder
    public Restaurant(String name,String description, String tel,String menu, String address, String category, String location) {
        this.name = name;
        this.description = description;
        this.tel = tel;
        this.address = address;
        this.menu = menu;
        this.category = category;
        this.location = location;
    }
}