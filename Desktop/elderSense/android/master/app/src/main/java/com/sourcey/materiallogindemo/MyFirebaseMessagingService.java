package com.sourcey.materiallogindemo;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.support.v4.app.NotificationCompat;
import android.util.Log;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;
import com.sourcey.materiallogindemo.MainActivity;
import com.sourcey.materiallogindemo.R;

import java.util.Map;

/**
 * Created by Kzhan00b on 1/7/2017.
 */

public class MyFirebaseMessagingService extends FirebaseMessagingService {

    private static final String TAG = "MyFirebaseMsgService";

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        //http://stackoverflow.com/questions/22252065/refreshing-activity-on-receiving-gcm-push-notification

        Log.d(TAG, "FROM: " + remoteMessage.getFrom());

        if (remoteMessage.getNotification() != null){
            String msgBody = remoteMessage.getNotification().getBody();
            Log.d(TAG, "FROM: " + msgBody);

            if (msgBody.equalsIgnoreCase("elderAlert")){
                Intent intent = new Intent("elderAlert");
                this.sendBroadcast(intent);

            }else{
                if(remoteMessage.getData().size() > 0){
                    Map<String, String> msgData = remoteMessage.getData();

                    Intent intent = new Intent("familyAlert");
                    this.sendBroadcast(intent);
                }
            }
        }
    }


    //This method is only generating push notification
    //It is same as we did in earlier posts
    private void sendNotification(String messageBody) {
        Intent intent = new Intent(this, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_ONE_SHOT);

        //Set sound of notification
        Uri notificationSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder notifiBuilder = new NotificationCompat.Builder(this)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("Firebase Cloud Messaging")
                .setContentText(messageBody)
                .setAutoCancel(true)
                .setSound(notificationSound)
                .setContentIntent(pendingIntent);

        NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        notificationManager.notify(0, notifiBuilder.build());
    }

}
