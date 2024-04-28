package com.example.saferider;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface PaymentAPICall {
    @GET("https://upward-husky-marginally.ngrok-free.app/apis/fare-pay/{username}/{phone}/{amount}")
    Call<ResponsePay> getData(@Path("username") String username, @Path("phone")  String phone, @Path("amount") String amount);
}

