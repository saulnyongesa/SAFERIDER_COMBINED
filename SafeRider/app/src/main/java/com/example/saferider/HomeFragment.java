package com.example.saferider;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class HomeFragment extends Fragment {
    TextView name;
    Database dbHelper;
    private HomeAPICall apiCall;
    ProgressBar progressBar;
    Button emergencyButton;
    LocationManager locationManager;
    private static final int PERMISSION_REQUEST_CODE = 1001;
    Double lon, lat;

    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home, container, false);
        progressBar = view.findViewById(R.id.progressBar);
        dbHelper = new Database(getContext());
        name = view.findViewById(R.id.name);
        return view;
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        emergencyButton = view.findViewById(R.id.emButton);
        emergencyButton.setEnabled(false);
        emergencyButton.setOnClickListener(emergencyInit);
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://json.extendsclass.com/bin/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        apiCall = retrofit.create(HomeAPICall.class);
        UserDetails userDetails = getUserDetailsFromDatabase();
        String Name = userDetails.getName();
        name.setText(Name);

        locationManager = (LocationManager) requireActivity().getSystemService(Context.LOCATION_SERVICE);
        if (ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_COARSE_LOCATION)
                        != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(requireActivity(),
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION},
                    PERMISSION_REQUEST_CODE);
        } else {
            getLocation();
        }
    }

    private final View.OnClickListener emergencyInit = new View.OnClickListener() {
        @Override
        public void onClick(View v) {

            UserDetails userDetails = getUserDetailsFromDatabase();
            String username = userDetails.getUsername();
            progressBar.setVisibility(View.VISIBLE);

            Call<ResponseHome> call = apiCall.getData(username, lon.toString(), lat.toString());

            call.enqueue(new Callback<ResponseHome>() {
                @Override
                public void onResponse(@NonNull Call<ResponseHome> call, @NonNull Response<ResponseHome> response) {
                    progressBar.setVisibility(View.INVISIBLE);
                    Toast.makeText(getActivity(), "Emergency trigger initialized successful", Toast.LENGTH_LONG).show();
                }

                @Override
                public void onFailure(@NonNull Call<ResponseHome> call, @NonNull Throwable t) {
                    progressBar.setVisibility(View.INVISIBLE);
                    Toast.makeText(getActivity(), "Failed to initiate Emergency", Toast.LENGTH_LONG).show();
                }
            });
        }
    };

    private void getLocation() {
        LocationListener locationListener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {
                lat = location.getLatitude();
                lon = location.getLongitude();
                emergencyButton.setEnabled(true);
            }
            @Override
            public void onStatusChanged(String provider, int status, Bundle extras) {
            }
            @Override
            public void onProviderEnabled(@NonNull String provider) {
            }
            @Override
            public void onProviderDisabled(@NonNull String provider) {
            }
        };
        if (ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER,
                0, 0, locationListener);
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
