package com.example.knueats.controller;

import com.example.knueats.entity.*;
import com.example.knueats.entity.Menu;
import com.example.knueats.service.GeoService;
import org.json.simple.JSONArray;
import org.json.simple.parser.ParseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.domain.Example;
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
    MenuSearchRepository menuSearchRepository;
    @Autowired
    RestaurantSearchRepository restaurantSearchRepository;
    @Autowired
    GeoService geoService;
    @PostMapping("/")
    public Restaurant create(@RequestBody RestaurantInfo restaurantInfo) throws ParseException {
        String addr = restaurantInfo.getAddress();
        String json = geoService.getKakaoApiFromAddress(addr);
        ArrayList<Float> pos = geoService.changeToJSON(json);
        restaurantInfo.setLon(pos.get(0));
        restaurantInfo.setLat(pos.get(1));
        Restaurant restaurant = new Restaurant(
                restaurantInfo.getName(),
                restaurantInfo.getDescription(),
                restaurantInfo.getTel(),
                restaurantInfo.getLat(),
                restaurantInfo.getLon(),
                restaurantInfo.getAddress(),
                restaurantInfo.getCategory(),
                restaurantInfo.getLocation(),
                restaurantInfo.getScore(),
                restaurantInfo.getReview());
        restaurantRepository.save(restaurant);
        for (Menu menu : restaurantInfo.getMenu()){
            Menu menuInput = new Menu(restaurant.getId(),menu.getName(),menu.getPrice());
            menuRepository.save(menuInput);
        }
        return restaurant;
    }
    @GetMapping("/{id}")
    public RestaurantInfo detail(@PathVariable Long id){
        Restaurant restaurantInfo = restaurantRepository.findById(id).orElse(null);
        List<Menu> menu = menuRepository.findMenu(id);
        RestaurantInfo restaurant = new RestaurantInfo(
                restaurantInfo.getName(),
                restaurantInfo.getDescription(),
                restaurantInfo.getTel(),
                restaurantInfo.getAddress(),
                restaurantInfo.getLat(),
                restaurantInfo.getLon(),
                restaurantInfo.getLocation(),
                menu,
                restaurantInfo.getCategory(),
                restaurantInfo.getScore(),
                restaurantInfo.getReview());
        return restaurant;
    }

    @GetMapping("/category/{category}")
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
    @GetMapping("/search/")
    public List<Restaurant> search(@RequestParam(value="word") String word){
        String inputs = "%"+word+"%";
        List<Restaurant> restaurantList = restaurantSearchRepository.findContainedRestaurant(inputs);
        List<Long> menuList = menuSearchRepository.findContainedMenu(inputs);
        List<Restaurant> returnList = new ArrayList<>();
        for(Restaurant restaurant : restaurantList) {
            returnList.add(restaurant);
        }
        for(Long menu: menuList){
            Restaurant restaurant = restaurantRepository.findByRestaurantId(menu);
            returnList.add(restaurant);
        }
        return returnList;
    }
    @GetMapping("/location/{location}")
    public List<Restaurant> locationList(@PathVariable String location){
        List<Restaurant> restaurantList = restaurantRepository.findAll();
        List<Restaurant> returnList = new ArrayList<>();
        for(Restaurant restaurant : restaurantList){
            if(location.equals(restaurant.getLocation())){
                returnList.add(restaurant);
            }
        }
        return returnList;
    }
}
