package com.example.saferider;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface ProfileAPICall {
    // as we are making a get request specifying annotation as get and adding a url end point to it.
    @GET("https://upward-husky-marginally.ngrok-free.app/apis/{username}")
    // on below line specifying the method name which we have to call.
    Call<ResponseProfile> getData(@Path("username") String username);
}