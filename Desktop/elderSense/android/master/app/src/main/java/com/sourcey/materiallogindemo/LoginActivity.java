package com.sourcey.materiallogindemo;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.messaging.FirebaseMessaging;

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
import java.util.concurrent.ExecutionException;

import butterknife.Bind;
import butterknife.ButterKnife;

public class LoginActivity extends AppCompatActivity {
    private static final String TAG = "LoginActivity";
    private static final int REQUEST_SIGNUP = 0;

    @Bind(R.id.inputNumber) EditText _phoneNumber;
    @Bind(R.id.inputPassword) EditText _passwordText;
    @Bind(R.id.btn_login) Button _loginButton;
    @Bind(R.id.link_signup) TextView _signupLink;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        ButterKnife.bind(this);

        _loginButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                login();
            }
        });

        _signupLink.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                // Start the Signup activity
                //Intent intent = new Intent(getApplicationContext(), SignupActivity.class);
                Intent intent = new Intent(getApplicationContext(), elderPageActivity.class);
                startActivityForResult(intent, REQUEST_SIGNUP);
                finish();
                overridePendingTransition(R.anim.push_left_in, R.anim.push_left_out);
            }
        });
    }

    public void login() {
        Log.d(TAG, "Login");

        if (!validate()) {
            onLoginFailed();
            return;
        }

        _loginButton.setEnabled(false);

        final ProgressDialog progressDialog = new ProgressDialog(LoginActivity.this,
                R.style.AppTheme_Dark_Dialog);
        progressDialog.setIndeterminate(true);
        progressDialog.setMessage("Authenticating...");
        progressDialog.show();

        String phoneNumber = _phoneNumber.getText().toString();
        String password = _passwordText.getText().toString();
        //http://stackoverflow.com/questions/3075009/android-how-can-i-pass-parameters-to-asynctasks-onpreexecute
        String loginParams[] = {phoneNumber, password};
        try {
            Log.d(TAG, "WEW : ");
            String loginResponse = new connectHttp().execute(loginParams).get();
            Log.d(TAG, "loginResponse : " + loginResponse);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        // TODO: Implement your own authentication logic here.

        new android.os.Handler().postDelayed(
                new Runnable() {
                    public void run() {
                        progressDialog.dismiss();
                        // On complete call either onLoginSuccess or onLoginFailed
                        onLoginSuccess();
                         //onLoginFailed();

                    }
                }, 3000);
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_SIGNUP) {
            if (resultCode == RESULT_OK) {

                // TODO: Implement successful signup logic here
                // By default we just finish the Activity and log them in automatically
                this.finish();
            }
        }
    }

    @Override
    public void onBackPressed() {
        // Disable going back to the MainActivity
        moveTaskToBack(true);
    }

    public void onLoginSuccess() {
        _loginButton.setEnabled(true);

        Intent intent = new Intent(getApplicationContext(), elderPageActivity.class);
        startActivityForResult(intent, REQUEST_SIGNUP);
        overridePendingTransition(R.anim.push_left_in, R.anim.push_left_out);
        finish();

//        Toast toast = Toast.makeText(this, "Should be okay", Toast.LENGTH_SHORT);
//        TextView v = (TextView) toast.getView().findViewById(android.R.id.message);
//        toast.show();
//        finish();
    }

    public void onLoginFailed() {
        //Toast.makeText(getBaseContext(), "Login failed, check if your number/password is correct!", Toast.LENGTH_LONG).show();
        //http://stackoverflow.com/questions/3522023/center-text-in-a-toast-in-android
        Toast toast = Toast.makeText(this, "Login Failed:\n" +
                "Check if Phone Number or Password is Correct", Toast.LENGTH_SHORT);
        TextView v = (TextView) toast.getView().findViewById(android.R.id.message);
        if ( v != null) v.setGravity(Gravity.CENTER);
        toast.show();

        _loginButton.setEnabled(true);
    }

    public boolean validate() {
        boolean valid = true;

        String phoneNumber = _phoneNumber.getText().toString();
        String password = _passwordText.getText().toString();

        if (phoneNumber.isEmpty() || !android.util.Patterns.PHONE.matcher(phoneNumber).matches()) {
            _phoneNumber.setError("Please enter a valid phone number.");
            valid = false;
        } else {
            _phoneNumber.setError(null);
        }

        if (password.isEmpty() || password.length() < 4 || password.length() > 10) {
            _passwordText.setError("between 4 and 10 alphanumeric characters");
            valid = false;
        } else {
            _passwordText.setError(null);
        }

        return valid;
    }//public boolean validate() method

    public class connectHttp extends AsyncTask<String, Object, String>{

        @Override
        protected String doInBackground(String... loginParams) {

            StringBuffer chaine = new StringBuffer("");
            try{
                //http://stackoverflow.com/questions/10116961/can-you-explain-the-httpurlconnection-connection-process
                URL url = new URL("http://10.0.2.2:8000/server/deviceLogin/");
                HttpURLConnection connection = (HttpURLConnection)url.openConnection();
                connection.setRequestMethod("POST");
                //connection.setRequestProperty("Content-Type","application/json; charset=utf-8");
                connection.setDoInput(true);
                connection.setDoOutput(true);
                connection.connect();

                //http://stackoverflow.com/questions/13911993/sending-a-json-http-post-request-from-android
                JSONObject jObject = new JSONObject();
                try {
                    jObject.put("Phone Number", loginParams[0]);
                    jObject.put("Password", loginParams[1]);

                    OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream());
                    out.write(jObject.toString());
                    out.close();
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
        }//doInBackground()

        @Override
        protected void onPostExecute(String arg){
            Log.d(TAG, "onPostExecute: " + arg);
            if (arg.equalsIgnoreCase("Valid Login")){

                final String token = FirebaseInstanceId.getInstance().getToken();
                Log.d(TAG, "Token: " + token);

                String registerParams[] = {_phoneNumber.getText().toString(), token};

                TokenService tokenService = new TokenService();
                String temp = tokenService.registerTokenInDB(registerParams);

//                if(!temp.equalsIgnoreCase("Error")){
//                    return("Login Success");
//                }
//                return("Token Registration Failed");
            }

//            return("Login Failed");
        }//onPostExecute()
    }//public connectHttp Class
}//public LoginActivity class
