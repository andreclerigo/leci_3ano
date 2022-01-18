typedef struct {
    char msg[1024];
} ServiceRequest;

typedef struct {
    int count;
    int alpha_count;
    int digit_count;
} ServiceResponse;

typedef struct {
    ServiceRequest req;
    ServiceResponse res;
} BUFFER;

void processService();
void callService(ServiceRequest* req, ServiceResponse* res);
