package com.example.knueats.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MenuSearchRepository extends JpaRepository<Menu,String> {
    @Query(value = "SELECT distinct(restaurant_id) from menu where name like :word", nativeQuery = true)
        List<Long> findContainedMenu(@Param("word") String word);
}
