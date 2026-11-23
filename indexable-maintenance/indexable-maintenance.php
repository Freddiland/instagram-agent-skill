<?php
/**
 * Plugin Name: Indexable Maintenance
 * Description: Modo mantenimiento que muestra la página de mantenimiento a los visitantes (HTTP 503) pero deja que los buscadores verificados (Googlebot, Bingbot, Applebot) rastreen e indexen el sitio real.
 * Version:     1.0.0
 * Author:      Alfredo
 * License:     GPL-2.0-or-later
 * Text Domain: indexable-maintenance
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

final class IMM_Indexable_Maintenance {

	const OPTION = 'imm_settings';

	/** Bots admitidos: regex del User-Agent => sufijos de rDNS válidos. */
	const BOTS = array(
		'googlebot|google-inspectiontool|adsbot-google|mediapartners-google|googleother' => array( '.googlebot.com', '.google.com', '.googleusercontent.com' ),
		'bingbot|adidxbot|bingpreview'                                                  => array( '.search.msn.com' ),
		'applebot'                                                                      => array( '.applebot.apple.com' ),
	);

	public static function init() {
		add_action( 'template_redirect', array( __CLASS__, 'maybe_block' ), 0 );
		add_action( 'admin_menu', array( __CLASS__, 'add_menu' ) );
		add_action( 'admin_init', array( __CLASS__, 'register_settings' ) );
		add_action( 'admin_bar_menu', array( __CLASS__, 'admin_bar' ), 100 );
	}

	/* ---------------------------------------------------------------- Ajustes */

	public static function defaults() {
		return array(
			'enabled'     => 0,
			'allow_bots'  => 1,
			'title'       => 'Sitio en mantenimiento',
			'message'     => 'Estamos realizando tareas de mantenimiento. Volvemos enseguida.',
			'retry_after' => 3600,
			'whitelist'   => '',
		);
	}

	public static function get() {
		return wp_parse_args( get_option( self::OPTION, array() ), self::defaults() );
	}

	public static function register_settings() {
		register_setting(
			'imm_group',
			self::OPTION,
			array(
				'type'              => 'array',
				'sanitize_callback' => array( __CLASS__, 'sanitize' ),
				'default'           => self::defaults(),
			)
		);
	}

	public static function sanitize( $in ) {
		$in  = is_array( $in ) ? $in : array();
		$out = array();

		$out['enabled']     = empty( $in['enabled'] ) ? 0 : 1;
		$out['allow_bots']  = empty( $in['allow_bots'] ) ? 0 : 1;
		$out['title']       = sanitize_text_field( $in['title'] ?? '' );
		$out['message']     = wp_kses_post( $in['message'] ?? '' );
		$out['retry_after'] = max( 60, min( 86400 * 7, absint( $in['retry_after'] ?? 3600 ) ) );

		// Lista de IPs: una por línea, solo IPs válidas.
		$ips = array();
		foreach ( preg_split( '/[\s,]+/', (string) ( $in['whitelist'] ?? '' ) ) as $ip ) {
			if ( $ip && filter_var( $ip, FILTER_VALIDATE_IP ) ) {
				$ips[] = $ip;
			}
		}
		$out['whitelist'] = implode( "\n", array_unique( $ips ) );

		return $out;
	}

	public static function add_menu() {
		add_options_page( 'Mantenimiento', 'Mantenimiento', 'manage_options', 'imm-settings', array( __CLASS__, 'render_page' ) );
	}

	public static function render_page() {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}
		$s = self::get();
		$o = self::OPTION;
		?>
		<div class="wrap">
			<h1>Modo mantenimiento indexable</h1>
			<form method="post" action="options.php">
				<?php settings_fields( 'imm_group' ); ?>
				<table class="form-table" role="presentation">
					<tr>
						<th scope="row">Activar mantenimiento</th>
						<td><label><input type="checkbox" name="<?php echo esc_attr( $o ); ?>[enabled]" value="1" <?php checked( $s['enabled'], 1 ); ?>> Mostrar página de mantenimiento a los visitantes</label></td>
					</tr>
					<tr>
						<th scope="row">Permitir buscadores</th>
						<td>
							<label><input type="checkbox" name="<?php echo esc_attr( $o ); ?>[allow_bots]" value="1" <?php checked( $s['allow_bots'], 1 ); ?>> Googlebot, Bingbot y Applebot ven el sitio real</label>
							<p class="description">Se verifica por DNS inverso + directo, no solo por User-Agent (el UA se falsifica trivialmente).</p>
						</td>
					</tr>
					<tr>
						<th scope="row"><label for="imm_title">Título</label></th>
						<td><input id="imm_title" class="regular-text" type="text" name="<?php echo esc_attr( $o ); ?>[title]" value="<?php echo esc_attr( $s['title'] ); ?>"></td>
					</tr>
					<tr>
						<th scope="row"><label for="imm_message">Mensaje</label></th>
						<td><textarea id="imm_message" class="large-text" rows="4" name="<?php echo esc_attr( $o ); ?>[message]"><?php echo esc_textarea( $s['message'] ); ?></textarea></td>
					</tr>
					<tr>
						<th scope="row"><label for="imm_retry">Retry-After (segundos)</label></th>
						<td><input id="imm_retry" type="number" min="60" name="<?php echo esc_attr( $o ); ?>[retry_after]" value="<?php echo esc_attr( $s['retry_after'] ); ?>"></td>
					</tr>
					<tr>
						<th scope="row"><label for="imm_wl">IPs con acceso</label></th>
						<td>
							<textarea id="imm_wl" class="large-text code" rows="3" name="<?php echo esc_attr( $o ); ?>[whitelist]"><?php echo esc_textarea( $s['whitelist'] ); ?></textarea>
							<p class="description">Una por línea (clientes, tu oficina). Los usuarios con sesión iniciada y permiso de edición siempre pasan.</p>
						</td>
					</tr>
				</table>
				<?php submit_button(); ?>
			</form>
			<p><strong>Tu IP detectada:</strong> <code><?php echo esc_html( self::client_ip() ); ?></code></p>
			<p class="description">Detrás de Cloudflare, asegúrate de que el servidor restaura la IP real en <code>REMOTE_ADDR</code> (mod_remoteip o plugin oficial de Cloudflare); si no, la verificación de bots fallará.</p>
		</div>
		<?php
	}

	public static function admin_bar( $bar ) {
		$s = self::get();
		if ( $s['enabled'] && current_user_can( 'manage_options' ) ) {
			$bar->add_node(
				array(
					'id'    => 'imm-active',
					'title' => 'Mantenimiento ACTIVO',
					'href'  => admin_url( 'options-general.php?page=imm-settings' ),
					'meta'  => array( 'class' => 'ab-item' ),
				)
			);
		}
	}

	/* ------------------------------------------------------------- Bloqueo */

	public static function maybe_block() {
		$s = self::get();
		if ( ! $s['enabled'] ) {
			return;
		}

		if ( self::should_bypass( $s ) ) {
			// Si hay caché de página, que no mezcle la versión real con la de mantenimiento.
			if ( ! defined( 'DONOTCACHEPAGE' ) ) {
				define( 'DONOTCACHEPAGE', true );
			}
			return;
		}

		self::render_maintenance( $s );
	}

	private static function should_bypass( array $s ) {
		if ( is_admin() || wp_doing_ajax() || wp_doing_cron() || ( defined( 'WP_CLI' ) && WP_CLI ) ) {
			return true;
		}
		if ( isset( $GLOBALS['pagenow'] ) && 'wp-login.php' === $GLOBALS['pagenow'] ) {
			return true;
		}
		if ( current_user_can( 'edit_posts' ) ) {
			return true;
		}

		$ip = self::client_ip();

		if ( $ip && in_array( $ip, preg_split( '/\s+/', trim( $s['whitelist'] ) ), true ) ) {
			return true;
		}

		if ( $s['allow_bots'] && self::is_verified_bot( $ip ) ) {
			return true;
		}

		return false;
	}

	public static function client_ip() {
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
		return (string) apply_filters( 'imm_client_ip', filter_var( $ip, FILTER_VALIDATE_IP ) ? $ip : '' );
	}

	private static function is_verified_bot( $ip ) {
		if ( ! $ip || empty( $_SERVER['HTTP_USER_AGENT'] ) ) {
			return false;
		}
		$ua = sanitize_text_field( wp_unslash( $_SERVER['HTTP_USER_AGENT'] ) );

		$suffixes = null;
		foreach ( self::BOTS as $pattern => $list ) {
			if ( preg_match( '/' . $pattern . '/i', $ua ) ) {
				$suffixes = $list;
				break;
			}
		}
		if ( null === $suffixes ) {
			return false;
		}

		// Caché por IP: evita DNS en cada petición del bot.
		$key    = 'imm_bot_' . md5( $ip . '|' . implode( ',', $suffixes ) );
		$cached = get_transient( $key );
		if ( false !== $cached ) {
			return '1' === $cached;
		}

		$ok   = false;
		$host = @gethostbyaddr( $ip ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
		if ( $host && $host !== $ip ) {
			$host = strtolower( $host );
			foreach ( $suffixes as $suffix ) {
				if ( substr( $host, -strlen( $suffix ) ) === $suffix ) {
					// DNS directo: el host debe resolver a la misma IP.
					$ok = in_array( $ip, self::resolve( $host ), true );
					break;
				}
			}
		}

		set_transient( $key, $ok ? '1' : '0', $ok ? DAY_IN_SECONDS : HOUR_IN_SECONDS );
		return $ok;
	}

	private static function resolve( $host ) {
		$ips = array();
		if ( function_exists( 'dns_get_record' ) ) {
			$records = @dns_get_record( $host, DNS_A | DNS_AAAA ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
			foreach ( (array) $records as $r ) {
				if ( ! empty( $r['ip'] ) ) {
					$ips[] = $r['ip'];
				}
				if ( ! empty( $r['ipv6'] ) ) {
					$ips[] = $r['ipv6'];
				}
			}
		}
		if ( ! $ips ) {
			$ips = (array) @gethostbynamel( $host ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
		}
		return $ips;
	}

	private static function render_maintenance( array $s ) {
		if ( ! defined( 'DONOTCACHEPAGE' ) ) {
			define( 'DONOTCACHEPAGE', true );
		}
		nocache_headers();
		status_header( 503 );
		header( 'Retry-After: ' . (int) $s['retry_after'] );
		header( 'Content-Type: text/html; charset=utf-8' );
		?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="robots" content="noindex, nofollow">
	<title><?php echo esc_html( $s['title'] ); ?></title>
	<style>
		body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;font:16px/1.6 system-ui,sans-serif;background:#f6f7f9;color:#1d2327;text-align:center;padding:24px}
		main{max-width:520px}
		h1{font-size:1.8rem;margin:0 0 .5em}
	</style>
</head>
<body>
	<main>
		<h1><?php echo esc_html( $s['title'] ); ?></h1>
		<div><?php echo wp_kses_post( wpautop( $s['message'] ) ); ?></div>
	</main>
</body>
</html>
		<?php
		exit;
	}
}

IMM_Indexable_Maintenance::init();
