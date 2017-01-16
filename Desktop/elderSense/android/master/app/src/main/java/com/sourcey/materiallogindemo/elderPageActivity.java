package com.sourcey.materiallogindemo;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.view.animation.LinearInterpolator;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.iid.FirebaseInstanceId;

import butterknife.Bind;
import io.github.douglasjunior.androidSimpleTooltip.SimpleTooltip;

//KIV for UI design?
//http://frogermcs.github.io/InstaMaterial-concept-part-6-user-profile/

public class elderPageActivity extends AppCompatActivity implements View.OnClickListener {

    static Boolean alertState = null;

    @Bind(R.id.infoButton) Button _infoButton;
    @Bind(R.id.flashButton) Button _flashButton;
    @Bind(R.id.testButton) Button _testButton;
    //https://github.com/douglasjunior/android-simple-tooltip/blob/master/sample/src/main/java/io/github/douglasjunior/androidSimpleTooltip/sample/MainActivity.java
    //https://github.com/douglasjunior/android-simple-tooltip

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_elder_page);

        if (alertState == null){
            alertState = false;
            findViewById(R.id.flashButton).setEnabled(false);
            //_flashButton.setEnabled(false);
        }

        setActionBar();

        //View yourView = findViewById(R.id.activity_elder_page);
        findViewById(R.id.testButton).setOnClickListener(elderPageActivity.this);
        findViewById(R.id.infoButton).setOnClickListener(elderPageActivity.this);
        findViewById(R.id.flashButton).setOnClickListener(elderPageActivity.this);


    }//onCreate()

    @Override
    public void onResume(){
        super.onResume();
        this.registerReceiver(mMessageReceiver, new IntentFilter("elderAlert"));
    }//onResume()

    @Override
    protected void onPause() {
        super.onPause();
        this.unregisterReceiver(mMessageReceiver);
    }

    //This is the handler that will manager to process the broadcast intent
    //http://stackoverflow.com/questions/22252065/refreshing-activity-on-receiving-gcm-push-notification
    private BroadcastReceiver mMessageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {

            // Extract data included in the Intent
            String message = intent.getStringExtra("message");

            flashButton();
            //do other stuff here
        }
    };

    public void setActionBar(){
        //KIV to add overflow menu for future?
        //https://developer.android.com/training/appbar/actions.html
        //https://developer.android.com/training/appbar/setting-up.html
        Toolbar myToolbar = (Toolbar) findViewById(R.id.my_toolbar);
        setSupportActionBar(myToolbar);

        ActionBar test = getSupportActionBar();
        //http://stackoverflow.com/questions/3438276/change-title-bar-text-in-android
        test.setTitle("Elder Page");
        test.setBackgroundDrawable(new ColorDrawable(getResources().getColor(R.color.primary_dark)));
        return;
    }//setActionBar()

    @Override
    public void onClick(final View view) {
        if (view.getId() == R.id.infoButton){

            new SimpleTooltip.Builder(this)
                    .anchorView(findViewById(R.id.testButton))
                    .text("Hello it's me")
                    .gravity(Gravity.START)
                    .animated(true)
                    .transparentOverlay(false)
                    .build()
                    .show();

        }else if(view.getId() == R.id.testButton){
//            final String TAG = "elderPageActivity";
//            String token = FirebaseInstanceId.getInstance().getToken();
//            Log.d(TAG, "Token: " + token);
//            Toast.makeText(elderPageActivity.this, token, Toast.LENGTH_SHORT).show();

            flashButton();

        }else if(view.getId() == R.id.flashButton){
            noFlashButton();
        }
    }//onClick()

    private void flashButton(){
        //http://stackoverflow.com/questions/4852281/android-how-can-i-make-a-button-flash
        final Animation animation = new AlphaAnimation(1, 0);
        animation.setDuration(500);
        animation.setInterpolator(new LinearInterpolator());
        animation.setRepeatCount(Animation.INFINITE);
        animation.setRepeatMode(Animation.REVERSE);

        Button tempView = (Button) findViewById(R.id.flashButton);

        tempView.setEnabled(true);
        tempView.startAnimation(animation);
        tempView.setText("Click here if you are okay!");

        //findViewById(R.id.flashButton).setEnabled(true);
        //findViewById(R.id.flashButton).startAnimation(animation);
    }//flashButton()

    private void noFlashButton(){
        Button tempView = (Button) findViewById(R.id.flashButton);
        tempView.setText("Nothing is up!");
        tempView.setEnabled(false);
        tempView.clearAnimation();
    }//noFlashButton()

}//elderPageActivity class
