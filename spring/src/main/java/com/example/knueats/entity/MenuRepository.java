package com.example.knueats.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MenuRepository extends JpaRepository<Menu, Long> {
    @Query(value = "select * from menu where restaurant_id = :id",nativeQuery = true)
        List<Menu> findMenu(@Param("id") Long id);
    Menu save(Menu menu);
}
