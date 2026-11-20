
import posixpath

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.crypto import get_random_string

from supabase import create_client


class SupabaseStorage(Storage):

    def __init__(self, bucket="noticias", public=True):
        self.bucket = bucket
        self.public = public
        self._client = None

    @property
    def client(self):
        if self._client is None:
            url = settings.SUPABASE_URL
            key = settings.SUPABASE_SERVICE_ROLE_KEY

            if not url or not key:
                raise ValueError(
                    "Configure SUPABASE_URL e "
                    "SUPABASE_SERVICE_ROLE_KEY no .env."
                )

            self._client = create_client(url, key)

        return self._client

    def get_available_name(self, name, max_length=None):
        folder, filename = posixpath.split(name)
        extension = posixpath.splitext(filename)[1]
        novo_nome = get_random_string(12) + extension

        if folder:
            return posixpath.join(folder, novo_nome)

        return novo_nome

    def _save(self, name, content):
        arquivo = b"".join(content.chunks())

        tipo = getattr(
            content,
            "content_type",
            "application/octet-stream"
        )

        self.client.storage.from_(self.bucket).upload(
            name,
            arquivo,
            file_options={
                "content-type": tipo,
                "upsert": "true"
            }
        )

        return name

    def _open(self, name, mode="rb"):
        resposta = self.client.storage.from_(
            self.bucket
        ).download(name)

        return ContentFile(resposta, name=name)

    def exists(self, name):
        return False

    def delete(self, name):
        if name:
            self.client.storage.from_(
                self.bucket
            ).remove([name])

    def url(self, name):
        armazenamento = self.client.storage.from_(
            self.bucket
        )

        if self.public:
            return armazenamento.get_public_url(name)

        resposta = armazenamento.create_signed_url(
            name,
            3600
        )

        if isinstance(resposta, dict):
            return (
                resposta.get("signedURL")
                or resposta.get("signedUrl")
            )

        return resposta
