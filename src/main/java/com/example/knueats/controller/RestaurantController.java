package com.example.knueats.controller;

import com.example.knueats.entity.Restaurant;
import com.example.knueats.entity.RestaurantDto;
import com.example.knueats.entity.RestaurantRepository;
import com.example.knueats.service.RestaurantService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/eats")
public class RestaurantController {
    RestaurantService restaurantService;
    @Autowired
    RestaurantRepository restaurantRepository;
    @PostMapping("/")
    public Restaurant create(@RequestBody Restaurant restaurant){
        return restaurantRepository.save(restaurant);
    }
    @GetMapping("/{category}")
    public List<Restaurant> list(@PathVariable String category){
        List<Restaurant> restaurantList = restaurantRepository.findAll();
        List<Restaurant> returnList = new ArrayList<>();
        for(Restaurant restaurant : restaurantList){
            if(category.equals(restaurant.getCategory())){
                returnList.add(restaurant);
            }
        }
        return returnList;
    }
    @GetMapping("/{category}/{id}")
    public  String detail(@PathVariable Long id){
        Optional<Restaurant> restaurantOptional = restaurantRepository.findById(id);
        restaurantOptional.ifPresent(System.out::println);
        return "success executed";
    }
    @GetMapping("/search")
    public List<Restaurant> search(@RequestParam(value="keyword") String keyword){
        List<Restaurant> restaurantList = restaurantRepository.findAll();
        List<Restaurant> returnList = new ArrayList<>();
        for(Restaurant restaurant : restaurantList){
            if(keyword.equals(restaurant.getName())||keyword.equals(restaurant.getMenu()))
                returnList.add(restaurant);
        }
        return returnList;
    }


}
