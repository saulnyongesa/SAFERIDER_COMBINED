package com.example.saferider;

import android.content.Intent;
import android.database.Cursor;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;


public class PaymentFragment extends Fragment {
    private PaymentAPICall apiCall;
    EditText phoneEditText, amountEditText;
    ProgressBar progressBar;
    Button payButton;
    Database dbHelper;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_payment, container, false);
        dbHelper = new Database(getContext());
        phoneEditText = view.findViewById(R.id.phone);
        amountEditText = view.findViewById(R.id.amount);
        progressBar = view.findViewById(R.id.progressBar);
        return view;
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        payButton = view.findViewById(R.id.payButton);
        payButton.setOnClickListener(payInit);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://json.extendsclass.com/bin/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        apiCall = retrofit.create(PaymentAPICall.class);
    }

    private String getUsernameFromDatabase() {
        String username = "";
        if (dbHelper != null) {
            Cursor cursor = dbHelper.getReadableDatabase().query(
                    "user_details", // Table name
                    new String[]{"username"}, // Columns to retrieve
                    "login_status = ?", // Selection
                    new String[]{"1"}, // Selection args (where login_status = 1)
                    null,
                    null,
                    null
            );

            if (cursor != null && cursor.moveToFirst()) {
                // Retrieve username from the cursor
                username = cursor.getString(cursor.getColumnIndexOrThrow("username"));
                cursor.close();
            }
        }
        return username;
    }

    private final View.OnClickListener payInit = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            String username = getUsernameFromDatabase();
            String phone = phoneEditText.getText().toString();
            String amount = amountEditText.getText().toString().trim();
            if (phone.startsWith("07") || phone.startsWith("01")) {
                phone = "254" + phone.substring(1);
            }
            else if (phone.startsWith("254")) {

            } else {
                Toast.makeText(getActivity(), "Invalid phone number format", Toast.LENGTH_LONG).show();
                return; // Stop further processing
            }
            progressBar.setVisibility(View.VISIBLE);
            Call<ResponsePay> call = apiCall.getData(username, phone, amount);
            call.enqueue(new Callback<ResponsePay>() {
                @Override
                public void onResponse(@NonNull Call<ResponsePay> call, @NonNull Response<ResponsePay> response) {
                    progressBar.setVisibility(View.INVISIBLE);
                    Toast.makeText(getActivity(), "Payment initiated successfully", Toast.LENGTH_LONG).show();
                    // Navigate to the HomeFragment
                    FragmentManager fragmentManager = requireActivity().getSupportFragmentManager();
                    FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                    fragmentTransaction.replace(R.id.frame_layout, new PaymentFragment());
                    fragmentTransaction.commit();
                }

                @Override
                public void onFailure(@NonNull Call<ResponsePay> call, @NonNull Throwable t) {
                    progressBar.setVisibility(View.INVISIBLE);
                    Toast.makeText(getActivity(), "Failed to initiate payment", Toast.LENGTH_LONG).show();
                }
            });
        }
    };
}
