from fastapi import HTTPException, status
from psycopg.errors import OperationalError, Error
from ..core.config import conn
from ..models.notification import NotificationResponse
from uuid import UUID

def get_all_notifications(user_id: UUID) -> list[NotificationResponse]:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT notification_id, user_id, message, is_read, created_at, updated_at
        FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
      """,
      (user_id,)
    )
    # ftech all tuples
    rows = cursor.fetchall()

    return [
      NotificationResponse(
        notification_id=row[0],
        user_id=row[1],
        message=row[2],
        is_read=row[3],
        created_at=row[4],
        updated_at=row[5]
      )
      for row in rows
    ]

  except OperationalError as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Database unavailable"
    )
  
  except Error as e:
    conn.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error"
    )
  
  finally:
    cursor.close()

def read_all_notifications(user_id: UUID) -> list[NotificationResponse]:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        UPDATE notifications
        SET is_read = TRUE, updated_at = NOW()
        WHERE user_id = %s
        RETURNING notification_id, user_id, message, is_read, created_at, updated_at
      """,
      (user_id,)
    )
    # fetch all tuples
    rows = cursor.fetchall()
    conn.commit()

    return [
      NotificationResponse(
        notification_id=row[0],
        user_id=row[1],
        message=row[2],
        is_read=row[3],
        created_at=row[4],
        updated_at=row[5]
      )
      for row in rows
    ]

  except OperationalError as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Database unavailable"
    )
  
  except Error as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error"
    )
  
  finally:
    cursor.close()

def delete_all_notifications(user_id: UUID) -> dict:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        DELETE FROM notifications
        WHERE user_id = %s
      """,
      (user_id,)
    )

    deleted_count = cursor.rowcount
    conn.commit()

    return {
      "message": "Notifications deleted",
      "deleted_count": deleted_count
    }

  except OperationalError as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Database unavailable"
    )
  
  except Error as e:
    conn.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error"
    )
  
  finally:
    cursor.close()

def get_notification(notification_id: UUID, user_id: UUID) -> NotificationResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT notification_id, user_id, message, is_read, created_at, updated_at
        FROM notifications
        WHERE notification_id = %s AND user_id = %s
      """,
      (notification_id, user_id)
    )

    row = cursor.fetchone()

    if row is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Notification not found"
      )

    return NotificationResponse(
      notification_id=row[0],
      user_id=row[1],
      message=row[2],
      is_read=row[3],
      created_at=row[4],
      updated_at=row[5]
    )

  except OperationalError as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Database unavailable"
    )
  
  except Error as e:
    conn.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error"
    )
  
  finally:
    cursor.close()

def read_notification(notification_id: UUID, user_id: UUID) -> NotificationResponse:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        UPDATE notifications
        SET is_read = TRUE, updated_at = NOW()
        WHERE notification_id = %s AND user_id = %s
        RETURNING notification_id, user_id, message, is_read, created_at, updated_at
      """,
      (notification_id, user_id)
    )

    row = cursor.fetchone()

    if row is None:
      conn.rollback()
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Notification not found"
      )

    conn.commit()

    return NotificationResponse(
      notification_id=row[0],
      user_id=row[1],
      message=row[2],
      is_read=row[3],
      created_at=row[4],
      updated_at=row[5]
    )

  except OperationalError as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Database unavailable"
    )
  
  except Error as e:
    conn.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error"
    )
  
  finally:
    cursor.close()

def delete_notification(notification_id: UUID, user_id: UUID) -> dict:
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        DELETE FROM notifications
        WHERE notification_id = %s AND user_id = %s
      """,
      (notification_id, user_id)
    )

    if cursor.rowcount == 0:
      conn.rollback()
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Notification not found"
      )

    conn.commit()

    return {
      "message": "Notification deleted"
    }

  except OperationalError as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Database unavailable"
    )
  
  except Error as e:
    conn.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error"
    )
  
  finally:
    cursor.close()

def create_notification(event: dict):
  cursor = conn.cursor()

  try:
    if event["event"] == "payment.successful":
      sender_id = UUID(event["sender_id"])
      receiver_id = UUID(event["receiver_id"])
      amount = event["amount"]

      notifications = [
        (sender_id, f"₹{amount} sent successfully."),
        (receiver_id, f"₹{amount} received.")
      ]

    elif event["event"] == "payment.pending":
      sender_id = UUID(event["sender_id"])
      amount = event["amount"]

      notifications = [
        (sender_id, f"Your payment of ₹{amount} is pending.")
      ]

    elif event["event"] == "payment.failed":
      sender_id = UUID(event["sender_id"])
      amount = event["amount"]

      notifications = [
        (sender_id, f"Your payment of ₹{amount} failed.")
      ]

    elif event["event"] in ["refund.successful", "refund.completed"]:
      sender_id = UUID(event["sender_id"])
      amount = event["amount"]

      notifications = [
        (sender_id, f"₹{amount} has been refunded to your wallet.")
      ]

    elif event["event"] == "refund.failed":
      sender_id = UUID(event["sender_id"])
      amount = event["amount"]

      notifications = [
        (sender_id, f"Your refund of ₹{amount} failed.")
      ]

    elif event["event"] == "wallet.recharge.successful":
      user_id = UUID(event["user_id"])
      amount = event["amount"]

      notifications = [
        (user_id, f"Your wallet recharge of ₹{amount} was successful.")
      ]

    elif event["event"] == "wallet.recharge.failed":
      user_id = UUID(event["user_id"])
      amount = event["amount"]

      notifications = [
        (user_id, f"Your wallet recharge of ₹{amount} failed.")
      ]

    elif event["event"] == "wallet.withdraw.successful":
      user_id = UUID(event["user_id"])
      amount = event["amount"]

      notifications = [
        (user_id, f"Your withdrawal of ₹{amount} was successful.")
      ]

    elif event["event"] == "wallet.withdraw.failed":
      user_id = UUID(event["user_id"])
      amount = event["amount"]

      notifications = [
        (user_id, f"Your withdrawal of ₹{amount} failed.")
      ]

    elif event["event"] == "user.created":
      user_id = UUID(event["user_id"])

      notifications = [
        (user_id, "Your account has been created successfully.")
      ]

    elif event["event"] == "user.logged.in":
      user_id = UUID(event["user_id"])

      notifications = [
        (user_id, "You logged in successfully.")
      ]

    else:
      return

    cursor.executemany(
      """
        INSERT INTO notifications (user_id, message)
        VALUES (%s, %s)
      """,
      notifications
    )

    conn.commit()

  except OperationalError as e:
    conn.rollback()
    print(repr(e))
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="Database unavailable"
    )

  except Error as e:
    conn.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error"
    )

  finally:
    cursor.close()