package com.example.saferider;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import androidx.annotation.Nullable;

public class Database extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "user_details.db";
    private static final int DATABASE_VERSION = 1;
    public static final String TABLE_USER_DETAILS = "user_details";
    public static final String COLUMN_LOGIN_STATUS = "login_status";
    public static final String COLUMN_USERNAME = "username";
    public static final String COLUMN_NAME = "name";
    public static final String COLUMN_EMAIL = "email";
    public static final String COLUMN_PHONE = "phone";

    // Create table query
    private static final String SQL_CREATE_TABLE_USER_DETAILS = "CREATE TABLE " +
            TABLE_USER_DETAILS + "(" +
            COLUMN_LOGIN_STATUS + " INTEGER DEFAULT 0," +
            COLUMN_USERNAME + " TEXT," +
            COLUMN_NAME + " TEXT," +
            COLUMN_EMAIL + " TEXT," +
            COLUMN_PHONE + " TEXT" + ")";

    public Database(@Nullable Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(SQL_CREATE_TABLE_USER_DETAILS);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_USER_DETAILS);
        onCreate(db);
    }

    // Method to check if the user is logged in
    public boolean isUserLoggedIn() {
        SQLiteDatabase db = this.getReadableDatabase();
        String query = "SELECT * FROM " + TABLE_USER_DETAILS +
                " WHERE " + COLUMN_LOGIN_STATUS + " = 1";
        Cursor cursor = db.rawQuery(query, null);
        boolean isLoggedIn = cursor.getCount() > 0;
        cursor.close();
        db.close();
        return isLoggedIn;
    }
    public String userName() {
        SQLiteDatabase db = this.getReadableDatabase();
        String query = "SELECT * FROM " + TABLE_USER_DETAILS +
                " WHERE " + COLUMN_LOGIN_STATUS + " = 1";
        Cursor cursor = db.rawQuery(query, null);
        String username= String.valueOf(cursor.getCount() > 0);
        cursor.close();
        db.close();
        return username;
    }

    public void addUser(String username, String name, String email, String phone) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COLUMN_LOGIN_STATUS, 1); // Set login status to true by default
        values.put(COLUMN_USERNAME, username);
        values.put(COLUMN_NAME, name);
        values.put(COLUMN_EMAIL, email);
        values.put(COLUMN_PHONE, phone);
        db.insertWithOnConflict(TABLE_USER_DETAILS, null, values, SQLiteDatabase.CONFLICT_REPLACE);
        db.close();
    }

    public void deleteUserDetails() {
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(TABLE_USER_DETAILS, null, null);
        db.close();
    }
}
