package com.example.nier.rpicontroller;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


public class getUserName extends AppCompatActivity {

    private TextView DisplayIP;
    private TextView DisplayUN;
    private Button getUN;

    private String IP = "";
    private String URL = "";
    private String fileName = "username";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_get_user_name);

        DisplayIP = (TextView)findViewById(R.id.DisplayIP);
        DisplayUN = (TextView)findViewById(R.id.DisplayUN);
        getUN = (Button)findViewById(R.id.getUN);

        Bundle bundle = this.getIntent().getExtras();
        IP = bundle.getString("IP");
        DisplayIP.setText(IP);
        Toast.makeText(getUserName.this, "如要取得Username,請按住Hue Bridge的Button在按下GetUN的按鈕", Toast.LENGTH_LONG).show();
        getUN.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                setURL(IP);
                httpConnectionPost();
                setUserName();
            }
        });
    }

    private void setURL(String IP){
        URL = "http://" + IP + "/api";
    }

    private void httpConnectionPost(){
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    java.net.URL weburl = new URL(URL);
                    StringBuilder response = new StringBuilder();
                    HttpURLConnection conn = (HttpURLConnection) weburl.openConnection();
                    conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
                    conn.setRequestProperty("Accept", "application/json");
                    conn.setRequestMethod("POST");
                    conn.setDoInput(true); //允許輸入流，即允許下載
                    conn.setDoOutput(true); //允許輸出流，即允許上傳

                    JSONObject params = new JSONObject();
                    params.put("devicetype", "Hue_device");

                    Log.i("JSON", params.toString());
                    DataOutputStream writer = new DataOutputStream(conn.getOutputStream());
                    writer.writeBytes(params.toString());
                    writer.flush();
                    writer.close();

                    InputStream is = conn.getInputStream();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                    String line;

                    while ((line = reader.readLine()) != null) {
                        response.append(line);
                        response.append('\r');
                    }
                    reader.close();

                    Log.i("STATUS", String.valueOf(conn.getResponseCode()));
                    Log.i("MSG", conn.getResponseMessage());

                    conn.disconnect();

                    JSONArray jsonArray = new JSONArray(response.toString());
                    for(int i = 0; i < jsonArray.length(); i++){
                        JSONObject jsonObject =  jsonArray.getJSONObject(i);
                        Object jsonOb = jsonObject.getJSONObject("success").get("username");
                        Log.i("JSON", jsonOb.toString());
                        try {
                            FileOutputStream outputStream = openFileOutput(fileName, Context.MODE_PRIVATE);
                            outputStream.write(jsonOb.toString().getBytes());
                            outputStream.close();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
        thread.start();
    }

    private void setUserName(){
        try{
            FileInputStream inputStream = openFileInput(fileName);
            byte[] bytes = new byte[1024];
            StringBuffer sb = new StringBuffer();
            while (inputStream.read(bytes) != -1){
                sb.append(new String(bytes));
            }
            DisplayUN.setText(sb.toString());
            inputStream.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
