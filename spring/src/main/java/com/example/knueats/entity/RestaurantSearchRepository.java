package com.example.knueats.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface RestaurantSearchRepository extends JpaRepository<Restaurant,String> {
    @Query(value = "select * from restaurant where name like :word",nativeQuery = true)
    List<Restaurant> findContainedRestaurant(@Param("word") String word);
}
