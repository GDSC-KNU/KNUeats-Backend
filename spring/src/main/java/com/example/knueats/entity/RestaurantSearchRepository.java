package com.example.knueats.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface RestaurantSearchRepository extends JpaRepository<Restaurant,String> {
    @Query(value = "select * from restaurant where name like :word",nativeQuery = true)
        List<Restaurant> findContainedRestaurant(@Param("word") String word);
    @Query(value = "select * from restaurant where location like :location", nativeQuery = true)
        List<Restaurant> findLocationalRestaurant(@Param("location") String location);
    @Query(value = "select * from restaurant where category = :category", nativeQuery = true)
        List<Restaurant> findCategoricalRestaurant(@Param("category") String category);
}
