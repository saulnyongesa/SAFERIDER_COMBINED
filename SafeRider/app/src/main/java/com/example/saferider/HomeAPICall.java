package com.example.saferider;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface HomeAPICall {
    @GET("https://upward-husky-marginally.ngrok-free.app/apis/emergency/{username}/{lon}/{lat}")
    Call<ResponseHome> getData(@Path("username") String username, @Path("lon") String lon, @Path("lat") String lat);
}
