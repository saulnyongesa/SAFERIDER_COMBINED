package com.example.saferider;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
public class ProfileFragment extends Fragment {
    Button logout_btn;
    ProgressBar progressBar;
    Database dbHelper;

    TextView username_text, name_text, email_text, phone_text;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_profile, container, false);
        logout_btn = view.findViewById(R.id.logoutBtn);
        username_text = view.findViewById(R.id.username);
        name_text = view.findViewById(R.id.name);
        email_text = view.findViewById(R.id.email);
        phone_text = view.findViewById(R.id.phone);
        progressBar = view.findViewById(R.id.progressBar);

        dbHelper = new Database(getContext());
        UserDetails userDetails = getUserDetailsFromDatabase();
        String username = userDetails.getUsername();
        username_text.setText(username);
        String Name = userDetails.getName();
        name_text.setText(Name);
        String Email = userDetails.getEmail();
        email_text.setText(Email);
        String Phone = userDetails.getPhone();
        phone_text.setText(Phone);

        logout_btn.setOnClickListener(v -> logoutUser());
        return view;
    }
    private void logoutUser() {
        progressBar.setVisibility(View.VISIBLE);
        // Delete user details from the database
        dbHelper.deleteUserDetails();
        // Navigate back to the login screen
        startActivity(new Intent(getActivity(), LoginActivity.class));
        requireActivity().finish(); // Finish the current activity (ProfileFragment)
    }

    private UserDetails getUserDetailsFromDatabase() {
        UserDetails userDetails = new UserDetails();
        if (dbHelper != null) {
            SQLiteDatabase db = dbHelper.getReadableDatabase();
            Cursor cursor = db.query(
                    "user_details", // Table name
                    new String[]{"username", "name", "email", "phone"}, // Columns to retrieve
                    "login_status = ?", // Selection
                    new String[]{"1"}, // Selection args (where login_status = 1)
                    null,
                    null,
                    null
            );

            if (cursor != null && cursor.moveToFirst()) {
                // Retrieve fields from the cursor
                userDetails.setUsername(cursor.getString(cursor.getColumnIndexOrThrow("username")));
                userDetails.setName(cursor.getString(cursor.getColumnIndexOrThrow("name")));
                userDetails.setEmail(cursor.getString(cursor.getColumnIndexOrThrow("email")));
                userDetails.setPhone(cursor.getString(cursor.getColumnIndexOrThrow("phone")));
                cursor.close();
            }
        }
        return userDetails;
    }

}