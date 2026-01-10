package com.example;

import java.sql.*;

public class PostgresClient {

    private static final String DB_URL = "jdbc:postgresql://localhost:5432/mock_dss_db";
    private static final String USER = "postgres";
    private static final String PASSWORD = "default_pass";

    public static void main(String[] args) {
        PostgresClient client = new PostgresClient();
        client.getSignatureCountForDay("2023-01-10");
        client.insertDocument();
    }

    public void getSignatureCountForDay(String day) {
        String query = "SELECT count(*) FROM signatures WHERE DATE(signed_at) = ?";
        try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASSWORD);
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, day);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                System.out.println("Signature count: " + rs.getInt(1));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void insertDocument() {
        String query = "INSERT INTO documents (document_id, content, created_at) VALUES (?, ?, NOW())";
        try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASSWORD);
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, "12345678");  // example document ID
            stmt.setString(2, "Some random content");
            stmt.executeUpdate();

            System.out.println("Document inserted successfully.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
