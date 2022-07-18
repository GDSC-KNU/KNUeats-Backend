package com.example.knueats.service;

import aj.org.objectweb.asm.TypeReference;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mysql.cj.xdevapi.JsonArray;
import com.mysql.cj.xdevapi.JsonParser;
import org.json.simple.JSONArray;
import org.json.simple.JSONAware;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;
import org.springframework.stereotype.Service;
import springfox.documentation.spring.web.json.Json;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service("geoService")
//@PropertySources({
//        @PropertySource("classpath:properties/env.properties")
//})
public class GeoService {
    public String getKakaoApiFromAddress(String roadFullAddr) {
        String apiKey = "20a781e1d7a2357890100797f1525c1b";
        String apiUrl = "https://dapi.kakao.com/v2/local/search/address.json";
        String jsonString = null;

        try {
            roadFullAddr = URLEncoder.encode(roadFullAddr, "UTF-8");

            String addr = apiUrl + "?query=" + roadFullAddr;

            URL url = new URL(addr);
            URLConnection conn = url.openConnection();
            conn.setRequestProperty("Authorization", "KakaoAK " + apiKey);

            BufferedReader rd = null;
            rd = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
            StringBuffer docJson = new StringBuffer();

            String line;

            while ((line = rd.readLine()) != null) {
                docJson.append(line);
            }

            jsonString = docJson.toString();
            rd.close();

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return jsonString;
    }
    public ArrayList changeToJSON(String jsonString) throws ParseException {
        ArrayList<Float> array = new ArrayList<Float>();
        JSONParser parser = new JSONParser();
        JSONObject document = (JSONObject)parser.parse(jsonString);
        JSONArray jsonArray = (JSONArray) document.get("documents");
        JSONObject position = (JSONObject)jsonArray.get(0);
        float lon = Float.parseFloat((String) position.get("x"));
        float lat = Float.parseFloat((String) position.get("y"));
        array.add(lon);
        array.add(lat);
        return array;
    }
}
