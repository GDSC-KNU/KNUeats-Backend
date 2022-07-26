package com.example.knueats.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface RestaurantSearchRepository extends JpaRepository<Restaurant,String> {
    @Query(value = "select id from restaurant where name like :word",nativeQuery = true)
        List<Long> findContainedRestaurantId(@Param("word") String word);
    @Query(value = "select * from restaurant where name like :word order by review DESC",nativeQuery = true)
        List<Restaurant> findContainedRestaurant(@Param("word") String word);
    @Query(value = "select * from restaurant where location like :location order by review DESC", nativeQuery = true)
        List<Restaurant> findLocationalRestaurantByReview(@Param("location") String location);
    @Query(value = "select * from restaurant where location like :location order by (score/review) DESC", nativeQuery = true)
    List<Restaurant> findLocationalRestaurantByScore(@Param("location") String location);
    @Query(value = "select * from restaurant where category = :category order by review DESC", nativeQuery = true)
        List<Restaurant> findCategoricalRestaurantByReview(@Param("category") String category);
    @Query(value = "select * from restaurant where category = :category order by (score/review) DESC", nativeQuery = true)
        List<Restaurant> findCategoricalRestaurantByScore(@Param("category") String category);
}
