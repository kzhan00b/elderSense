package com.sourcey.materiallogindemo;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutionException;

/**
 * Created by Kzhan00b on 1/8/2017.
 * https://github.com/carlosCharz/FCMTest/tree/master/app/src/main/java/com/wedevol/fcmtest
 */

public class TokenService {
    private static final String TAG = "TokenService";
    private static final String BACKEND_SERVER_IP = "10.0.2.2:8000/server";
    private static final String BACKEND_URL_BASE = "http://" + BACKEND_SERVER_IP;

    public String registerTokenInDB(final String[] token){
        try {
            Log.d(TAG, "BEFORE PASSING");
            String registrationResponse = new connectHttp().execute(token).get();
            Log.d(TAG, "AFTER PASSING");
            return registrationResponse;
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }

        return ("Error");
    }

    public class connectHttp extends AsyncTask<String, Object, String> {

        @Override
        protected String doInBackground(String... token) {

            StringBuffer chaine = new StringBuffer("");
            try{
                Log.d(TAG, "BEFORE CONNECT()");
                //URL url = new URL(BACKEND_URL_BASE + "/fcm/v1/devices/");
                URL url = new URL(BACKEND_URL_BASE + "/deviceRegisterToken/");
                HttpURLConnection connection = (HttpURLConnection)url.openConnection();
                connection.setRequestMethod("POST");
                connection.setDoInput(true);
                connection.setDoOutput(true);
                connection.connect();

                Log.d(TAG, "AFTER CONNECT()");

                //http://stackoverflow.com/questions/13911993/sending-a-json-http-post-request-from-android
                JSONObject jObject = new JSONObject();
                try {
                    jObject.put("dev_id", token[0].toString());
                    jObject.put("reg_id", token[1].toString());

                    Log.d(TAG, "BEFORE OUTPUTSTREAMWRITER");
                    OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream());
                    out.write(jObject.toString());
                    out.close();
                    Log.d(TAG, "AFTER OUTPUTSTREAMWRITER");
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                InputStream inputStream = connection.getInputStream();

                BufferedReader rd = new BufferedReader(new InputStreamReader(inputStream));
                String line = "";
                while ((line = rd.readLine()) != null) {
                    chaine.append(line);
                }
                return (chaine.toString());
            } catch (MalformedURLException e){
                e.printStackTrace();
            } catch (IOException e){
                e.printStackTrace();
            }
            return null;
        }//connectHttp()
    }//public connectHttp Class

}//TokenService class
