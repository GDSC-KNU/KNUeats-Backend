package com.example.knueats.controller;

import com.example.knueats.entity.Menu;
import com.example.knueats.entity.MenuRepository;
import com.example.knueats.entity.Restaurant;
import com.example.knueats.entity.RestaurantRepository;
import com.example.knueats.service.GeoService;
import org.json.simple.JSONArray;
import org.json.simple.parser.ParseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.*;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/eats")
public class RestaurantController {
    @Autowired
    RestaurantRepository restaurantRepository;
    @Autowired
    MenuRepository menuRepository;
    @Autowired
    GeoService geoService;
    @PostMapping("/")
    public Restaurant create(@RequestBody Restaurant restaurant) throws ParseException {
        String addr = restaurant.getAddress();
        String json = geoService.getKakaoApiFromAddress(addr);
        ArrayList<Float> pos = geoService.changeToJSON(json);
        restaurant.setLon(pos.get(0));
        restaurant.setLat(pos.get(1));
        return restaurantRepository.save(restaurant);
    }

    @GetMapping("/")
    public List<Restaurant> allList(){
        List<Restaurant> restaurantList = restaurantRepository.findAll();
        return restaurantList;
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
    @GetMapping("/search")
    public List<Restaurant> search(@RequestParam(value="word") String word){
        List<Restaurant> restaurantList = restaurantRepository.findAll();
        List<com.example.knueats.entity.Menu> menuList = menuRepository.findAll();
        List<Restaurant> returnList = new ArrayList<>();
        for(Restaurant restaurant : restaurantList){
            if(word.equals(restaurant.getName())) //검색 이름, 메뉴겹치면 반환
                returnList.add(restaurant);
        }
        for(Menu menu: menuList){
            if(word.equals(menu.getName())) {
                //해당 메뉴를 가진 레스토랑이 있다면 반환
                Restaurant restaurant = restaurantRepository.findById(menu.getRestaurantId()).orElse(null);
            }
        }
        return returnList;
    }
    //@GetMapping("/location/{location}")


}