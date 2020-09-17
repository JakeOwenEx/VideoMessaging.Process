

resource "aws_sns_topic" "video_messaging_processor_topic" {
  name = "video-messaging-processor-topic"
}

resource "aws_sqs_queue" "video_messaging_processor_queue" {
  name = "video-messaging-processor-queue"
}

resource "aws_sqs_queue_policy" "video_messaging_processor_qp" {
  queue_url = aws_sqs_queue.video_messaging_processor_queue.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.video_messaging_processor_queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.video_messaging_processor_topic.arn}"
        }
      }
    }
  ]
}
POLICY
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = aws_sns_topic.video_messaging_processor_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.video_messaging_processor_queue.arn
}
