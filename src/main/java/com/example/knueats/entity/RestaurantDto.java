package com.example.knueats.entity;

import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.Entity;
import javax.persistence.EntityListeners;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Getter
@Entity
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EntityListeners(AuditingEntityListener.class)
public class RestaurantDto {
    @Id
    @GeneratedValue
    private Long id;
    private String name;
    private String description;
    private String tel;
    private String address;
    private float lat;
    private float lon; //위도경도
    private String menu; //나중에 Menu menu로 변경
    private enum category {}

    public Restaurant toEntity() {
        Restaurant build = Restaurant.builder()
                .name(name)
                .tel(tel)
                .menu(menu)
                .lat(lat)
                .lon(lon)
                .build();
        return build;
    }

    @Builder
    public RestaurantDto(Restaurant entity) {
        this.name = entity.getName();
        this.tel = entity.getTel();
        this.menu = entity.getMenu();
        this.lat = entity.getLat();
        this.lon = entity.getLon();
    }
}
