package com.example.knueats.service;

import com.example.knueats.entity.Restaurant;
import com.example.knueats.entity.RestaurantDto;
import com.example.knueats.entity.RestaurantRepository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;


@Transactional(readOnly = true)
public class RestaurantService {
    private final RestaurantRepository restaurantRepository;

    public RestaurantService(RestaurantRepository restaurantRepository) {
        this.restaurantRepository = restaurantRepository;
    }
    @Transactional
    public Restaurant post(RestaurantDto restaurantDto) {
        return restaurantRepository.save(restaurantDto.toEntity());
    }

        //
    public List<RestaurantDto> findAll(){
        return restaurantRepository.findAll().stream()
                .map(RestaurantDto::new)
                .collect(Collectors.toList());
    }

    public RestaurantDto findById(Long id) {
        Restaurant entity = restaurantRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("해당 식당이 없습니다. id = " + id));
        return new RestaurantDto(entity);
    }
}