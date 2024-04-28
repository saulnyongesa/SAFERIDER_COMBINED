package com.example.saferider;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface LoginAPICall {
    @GET("https://upward-husky-marginally.ngrok-free.app/apis/login/{username}")
    // on below line specifying the method name which we have to call.
    Call<ResponseLogin> getData(@Path("username") String username);
}
