service MarvinService {
        string say_hello(),
        string say_echo(1: string str),
        bool send_file_request(1: string path, 2: string job_id, 3: string size),
        void send_chunk(1: string job_id, 2: binary chunk),
        void finish_sending(1: string job_id)
}
