package com.example.saferider;

import com.google.gson.annotations.SerializedName;

public class ResponsePay {
    @SerializedName("username")
    private String username;


    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }
}
