import java.io.*;
import java.net.*;

class Server {

    public static void main(String[] args) throws Exception {
       System.out.println("Starting server...");
       int port = 9876;
       try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Listening on http://localhost:" + port);
            while (true) {
                System.out.println("Waiting for client... ");
                try (Socket client = serverSocket.accept()) {
                    System.out.println("Debug: got new client " + client.toString());
                    BufferedReader br = new BufferedReader(new InputStreamReader(client.getInputStream()));

                    StringBuilder requestBuilder = new StringBuilder();
                    String line;
                    while (!(line = br.readLine()).isBlank()) {
                        requestBuilder.append(line + "\r\n");
                    }

                    String request = requestBuilder.toString();
                    System.out.println(request);

                    OutputStream clientOutput = client.getOutputStream();
                    clientOutput.write("HTTP/1.1 200 OK\r\n".getBytes());
                    clientOutput.write(("ContentType: text/html\r\n").getBytes());
                    clientOutput.write("\r\n".getBytes());
                    clientOutput.write("<html><body><h1>Hello World!</h1></body></html>".getBytes());
                    clientOutput.write("\r\n\r\n".getBytes());
                    clientOutput.flush();
                    client.close();

                    System.out.println("==============================================\n");

                }
            }
        }
    }

}