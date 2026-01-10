package com.example;

import okhttp3.*;

import java.io.IOException;

public class ApiLoadTest {

    private static final String API_URL = "http://localhost:8000";
    private static final OkHttpClient client = new OkHttpClient();

    public static void main(String[] args) throws IOException {
        getIndexPage();
        postSign();
    }

    public static void getIndexPage() throws IOException {
        Request request = new Request.Builder()
                .url(API_URL)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.code() == 200) {
                System.out.println("GET / success");
            } else {
                System.out.println("Failed: " + response.code());
            }
        }
    }

    public static void postSign() throws IOException {
        // Example payload for POST
        String json = "{ \"document_id\": \"1234\", \"payload\": \"Lorem ipsum\" }";

        RequestBody body = RequestBody.create(json, MediaType.get("application/json"));
        Request request = new Request.Builder()
                .url(API_URL + "/api/sign")
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.code() == 200) {
                System.out.println("POST /api/sign success");
            } else {
                System.out.println("Failed: " + response.code());
            }
        }
    }
}
