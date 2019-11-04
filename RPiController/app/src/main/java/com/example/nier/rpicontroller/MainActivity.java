package com.example.nier.rpicontroller;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    private Button OpenHue;
    private Button OpenAws;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        OpenHue = (Button)findViewById(R.id.openHue);
        OpenAws = (Button)findViewById(R.id.openAws);

        OpenHue.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent();
                intent.setClass(MainActivity.this, HueActivity.class);
                startActivity(intent);
            }
        });

        OpenAws.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent();
                intent.setClass(MainActivity.this, PubSubActivity.class);
                startActivity(intent);
            }
        });
    }
}
