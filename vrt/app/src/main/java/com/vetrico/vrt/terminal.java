package com.vetrico.vrt;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

public class terminal extends AppCompatActivity {


    Button query;
    EditText script;
    LinearLayout list;
    TextView tx , rtx;
    String scr , quit;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_terminal);

        Python py = Python.getInstance();
        PyObject Pyobj = py.getModule("script");


        query = (Button) findViewById(R.id.scr_submit);
        script = findViewById(R.id.script);
        list = (LinearLayout) findViewById(R.id.terminal_scroll);
        quit = "quit";
        query.setOnClickListener(new View.OnClickListener(){
           @Override
            public void onClick(View v)
           {
               try {
//                   PyObject test = Pyobj.callAttr("update" , script.getText().toString());
//                   scr = script.getText().toString();
                   backg test = new backg(terminal.this , Pyobj , script , query , list);
                   test.execute();
//                    if(script.getText().toString().equals(quit))
//                    {
//                        Intent inte = new Intent(terminal.this , auth.class);
//                        startActivity(inte);
//                    }
//                    else {
//                        tx = new TextView(getApplicationContext());
//                        tx.setText(script.getText().toString());
//                        tx.setPadding(10, 10, 10, 10);
//                        tx.setBackgroundColor(getResources().getColor(R.color.gray));
//                        list.addView(tx);
//                        rtx = new TextView(getApplicationContext());
//                        rtx.setPadding(10, 10, 10, 10);
//                        rtx.setText(test.toString());
//                        rtx.setBackgroundColor(getResources().getColor(R.color.white));
//                        list.addView(rtx);
//                        script.setText("");
//                    }
               }
               catch (Exception e)
               {
                   Intent inte = new Intent(terminal.this , MainActivity.class);
                   startActivity(inte);
               }



           }
        });
    }
    @Override
    public void onBackPressed() {
        // your code.
        Toast.makeText(terminal.this  , "press home directly" , Toast.LENGTH_LONG).show();
    }
}

