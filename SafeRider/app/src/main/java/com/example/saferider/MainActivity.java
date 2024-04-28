package com.example.saferider;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.os.Bundle;
import android.view.View;
import android.widget.ProgressBar;

import com.example.saferider.databinding.ActivityMainBinding;


public class MainActivity extends AppCompatActivity {
    ActivityMainBinding binding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        replaceFragment(new HomeFragment());
        binding.bottomNavView.setBackground(null);
        binding.bottomNavView.setOnItemSelectedListener(menuItem -> {
            if (menuItem.getItemId() == R.id.home) {
                replaceFragment(new HomeFragment());
            }
            else if (menuItem.getItemId() == R.id.payment) {
                replaceFragment(new PaymentFragment());
            }
            else if (menuItem.getItemId() == R.id.customer) {
                replaceFragment(new CustomerFragment());
            }
            else if (menuItem.getItemId() == R.id.profile) {
                replaceFragment(new ProfileFragment());
            }
            return true;
        });
    }

    private void replaceFragment(Fragment fragment){
        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
        fragmentTransaction.replace(R.id.frame_layout, fragment);
        fragmentTransaction.commit();
    }
}

