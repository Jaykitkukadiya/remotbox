package com.vetrico.vrt;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.chaquo.python.PyObject;

public class backg extends AsyncTask< Void , Void , String> {

    Context context;
    PyObject Pyobj , test;
//    ProgressDialog pg;
    Button query;
    EditText script;
    LinearLayout list;
    TextView tx , rtx;
    String scr , quit;
    backg(Context context , PyObject Pyobj , EditText script , Button query , LinearLayout list)
    {
        this.context = context;
        this.Pyobj = Pyobj;
        this.script = script;
        this.query = query;
        this.list = list;
    }
    @Override
    protected String doInBackground(Void... params) {
        try {
            test = Pyobj.callAttr("update" , scr);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "Tast completed";
    }
    @Override
    protected void onPostExecute(String result) {
//        pg.hide();
        quit = "quit";
        if(script.getText().toString().equals(quit))
        {
            context.startActivity(new Intent(context , auth.class));
        }
        else {
            tx = new TextView(context);
            tx.setText(scr);
            tx.setPadding(10, 10, 10, 10);
            tx.setBackgroundColor(Color.GRAY);
            list.addView(tx);
            rtx = new TextView(context);
            rtx.setPadding(10, 10, 10, 10);
            rtx.setText(test.toString());
            rtx.setBackgroundColor(Color.WHITE);
            list.addView(rtx);
            script.setText("");
        }
        query.setEnabled(true);
//        script.setText("");
        script.setEnabled(true);
        System.out.println("compleate");
    }
    @Override
    protected void onPreExecute() {
        scr = script.getText().toString();
        query.setEnabled(false);
        script.setText("wait for a while server is working......");
        script.setEnabled(false);
//        pg = new ProgressDialog(context);
//        pg.setTitle("loading ...");
        System.out.println("start");
//        pg.show();
    }
}
