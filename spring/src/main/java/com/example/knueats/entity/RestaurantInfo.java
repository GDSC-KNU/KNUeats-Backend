package com.example.knueats.entity;

import lombok.*;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import java.util.List;
@Getter
@Setter
public class RestaurantInfo {
    private String name;
    private String description;
    private String tel;
    private String address;
    private float lat;
    private float lon; //위도경도
    private String location;
    private List<Menu> menu; //나중에 Menu menu로 변경
    private String category;
    private float score;
    private int review;
    @Builder
    public RestaurantInfo(String name, String description, String tel, String address, float lat, float lon, String location, List<Menu> menu, String category, float score, int review) {
        this.name = name;
        this.description = description;
        this.tel = tel;
        this.address = address;
        this.category = category;
        this.location = location;
        this.menu = menu;
        this.lat = lat;
        this.lon = lon;
        this.score = score;
        this.review = review;

    }
}

