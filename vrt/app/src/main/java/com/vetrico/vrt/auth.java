package com.vetrico.vrt;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.IOException;

public class auth extends AppCompatActivity {

    EditText inp;
    Button lgn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_auth);
        inp = (EditText) findViewById(R.id.pass);
        lgn = (Button) findViewById(R.id.login);
//        Python.start(new AndroidPlatform(this));
        Python py = Python.getInstance();
        PyObject Pyobj = py.getModule("script");
        lgn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                PyObject obj = Pyobj.callAttr("main" , inp.getText());
                if(obj.toInt() == 1)
                {
                    Intent inte = new Intent(auth.this , terminal.class);
                    startActivity(inte);
                }
                else
                {
                Toast.makeText(auth.this , "invalid password" , Toast.LENGTH_LONG ).show();
                }
            }
        });


    }
    @Override
    public void onBackPressed() {
        Toast.makeText(auth.this  , "press home directly" , Toast.LENGTH_LONG).show();
    }
}
