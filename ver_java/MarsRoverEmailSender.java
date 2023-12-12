package emailApp;

import com.sendgrid.*;
import com.sendgrid.helpers.mail.Mail;
import com.sendgrid.helpers.mail.objects.*;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class MarsRoverEmailSender {
	
    private static final String TO_EMAIL = "cseryena03@gmail.com";
    private static final String FROM_EMAIL = "yc5103@nyu.edu";

    public static void main(String[] args) {
        try {
        	String apiKey = "xaMnzo8vv5GzmOWjhZ52ECba7w55t30PCEghILGI";
            String marsRoverPhotoUrl = getRandomNasaImage(apiKey);
            String emailContent = "Check out the latest Mars Rover photo!\n\n" + marsRoverPhotoUrl;
            System.out.print(emailContent);
           // sendEmail(emailContent);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String getRandomNasaImage(String apiKey) throws IOException {
        String apiUrl = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=301&page=2&api_key=" + apiKey;

        URL url = new URL(apiUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        Scanner scanner = new Scanner(connection.getInputStream());
        StringBuilder response = new StringBuilder();
        while (scanner.hasNextLine()) {
            response.append(scanner.nextLine());
        }
        scanner.close();

        String imageUrl = parseJsonResponse(response.toString());
        return imageUrl;
    }

    private static String parseJsonResponse(String jsonResponse)throws IOException {
        String imageUrl = jsonResponse.split("\"img_src\"")[1].split(",")[0].replace("}", "").trim();
        return imageUrl.substring(2, imageUrl.length()-1);
    }

    private static void sendEmail(String content) {
        Email from = new Email(FROM_EMAIL);
        String subject = "Latest Mars Rover Photo";
        Email to = new Email(TO_EMAIL);
        Content emailContent = new Content("text/plain", content);
        Mail mail = new Mail(from, subject, to, emailContent);

        SendGrid sg = new SendGrid(System.getenv("SENDGRID_API_KEY"));
        Request request = new Request();

        try {
            request.setMethod(Method.POST);
            request.setEndpoint("mail/send");
            request.setBody(mail.build());

            Response response = sg.api(request);
            System.out.println("Email sent successfully. Status Code: " + response.getStatusCode());
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}