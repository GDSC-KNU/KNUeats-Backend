package com.example.knueats.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface RestaurantRepository extends JpaRepository<Restaurant, Long> {
    List<Restaurant> findAll();
    @Query(value = "select * from restaurant where id=:input",nativeQuery = true)
        Restaurant findByRestaurantId(@Param("input") Long input);
    @Query(value = "update restaurant set score=:score,review=:review where id=:id",nativeQuery = true)
        Restaurant updateReview(@Param("score") Float score, @Param("review") int review, @Param("id") Long id);
    Restaurant save(Restaurant restaurant);

}
