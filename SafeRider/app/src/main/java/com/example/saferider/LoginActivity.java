package com.example.saferider;


import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class LoginActivity extends AppCompatActivity {

    private EditText usernameEditText;
    private EditText passwordEditText;
    private ProgressBar progressBar;
    private Button loginButton;
    private LoginAPICall apiCall;
    private Database dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        dbHelper = new Database(this);
        initializeViews();
        setupLoginButton();
    }

    private void initializeViews() {
        usernameEditText = findViewById(R.id.username);
        passwordEditText = findViewById(R.id.password);
        loginButton = findViewById(R.id.loginButton);
        progressBar = findViewById(R.id.progressBar);
    }

    private void setupLoginButton() {
        if (dbHelper.isUserLoggedIn()) {
            Toast.makeText(LoginActivity.this, "Already logged in!", Toast.LENGTH_SHORT).show();
            startActivity(new Intent(LoginActivity.this, MainActivity.class));
            finish(); // Finish LoginActivity to prevent going back to it from MainActivity
        } else {
            initializeRetrofit();
            loginButton.setOnClickListener(v -> loginUser());
        }
    }

    private void initializeRetrofit() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://json.extendsclass.com/bin/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        apiCall = retrofit.create(LoginAPICall.class);
    }

    private void loginUser() {
        String username = usernameEditText.getText().toString().trim();
        String password = passwordEditText.getText().toString();

        if (username.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "Please enter both username and password", Toast.LENGTH_SHORT).show();
            return;
        }

        progressBar.setVisibility(View.VISIBLE);

        Call<ResponseLogin> call = apiCall.getData(username);
        call.enqueue(new Callback<ResponseLogin>() {
            @Override
            public void onResponse(@NonNull Call<ResponseLogin> call, @NonNull Response<ResponseLogin> response) {
                if (response.isSuccessful() && response.body() != null) {
                    handleSuccessfulResponse(response.body(), username, password);
                } else {
                    handleFailedResponse();
                }
            }

            @Override
            public void onFailure(@NonNull Call<ResponseLogin> call, @NonNull Throwable t) {
                handleFailedResponse();
            }
        });
    }

    private void handleSuccessfulResponse(ResponseLogin responseData, String username, String password) {
        progressBar.setVisibility(View.INVISIBLE);
        if (password.equals(responseData.getPassword())) {
            String name = responseData.getFirstName() + " " + responseData.getSecondName() + " " + responseData.getLastName();
            String phone = responseData.getPhone();
            String email = responseData.getEmail();
            dbHelper.addUser(username, name, email, phone);
            startActivity(new Intent(LoginActivity.this, MainActivity.class));
            finish(); // Finish LoginActivity to prevent going back to it from MainActivity
            Toast.makeText(LoginActivity.this, "Logged in successful", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(LoginActivity.this, "Incorrect password", Toast.LENGTH_SHORT).show();
        }
    }

    private void handleFailedResponse() {
        progressBar.setVisibility(View.INVISIBLE);
        Toast.makeText(LoginActivity.this, "Failed to login. Please try again", Toast.LENGTH_SHORT).show();
    }
}


